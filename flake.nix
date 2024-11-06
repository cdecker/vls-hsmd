{
  description = "VLS nix development shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    naersk.url = "github:nix-community/naersk";
  };

  outputs = { self, nixpkgs, flake-utils, naersk }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        # build rust application :)
        naersk' = pkgs.callPackage naersk { };
      in
      rec {
        env = {
          SUBDAEMON = "hsmd:remote_hsmd_inplace";
        };
        # Set up the nix flake derivation
        packages = { };
        # FIXME: will be good to have this formatting also the rust code
        formatter = pkgs.nixpkgs-fmt;

        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [ pkg-config ];
          buildInputs = with pkgs; [
            git
            gnumake
            rustup

            openssl
            openssl.dev
            protobuf

            bitcoind

            # cln dependencies
            gcc
            sqlite
            autoconf
            git
            clang
            libtool
            sqlite
            autoconf
            autogen
            automake
            gnumake
            pkg-config
            gmp
            zlib
            gettext
            libsodium
            krb5
            openldap
            python3
            poetry
          ];
          shellHook = ''
            export HOST_CC=gcc
            export RUST_BACKTRACE=1

            poetry config virtualenvs.create false
            git checkout main
            git submodule update --init --recursive

            ./scripts/enable-githooks

            make build
          '';
        };
      }
    );
}
