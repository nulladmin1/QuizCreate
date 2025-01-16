{
  description = "QuizCreate";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.systems.follows = "nixpkgs";
    };
    systems.url = "github:nix-systems/default";
  };

  outputs = {
    nixpkgs,
    poetry2nix,
    systems,
    ...
  }: let
    forEachSystem = nixpkgs.lib.genAttrs (import systems);
    pkgsFor = forEachSystem (system: import nixpkgs {inherit system;});

    poetry2nix-lib = forEachSystem (system: poetry2nix.lib.mkPoetry2Nix {pkgs = pkgsFor.${system};});
  in {
    formatter = forEachSystem (system: nixpkgs.legacyPackages.${system}.alejandra);

    devShells = forEachSystem (system: {
      default =
        (poetry2nix-lib.${system}.mkPoetryEnv {
          projectDir = ./.;
          editablePackageSources = {
            quizcreate = ./quizcreate;
          };
        })
        .env
        .overrideAttrs (oldAttrs: {
          buildInputs = with pkgsFor.${system}; [
            poetry
          ];
        });
    });

    apps = forEachSystem (system: let
      quizcreate = poetry2nix-lib.${system}.mkPoetryApplication {projectDir = ./.;};
    in {
      default = {
        type = "app";
        program = "${quizcreate}/bin/quizcreate";
      };
    });
  };
}
