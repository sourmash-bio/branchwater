{ modulesPath, pkgs, ... }: {
  imports = [ "${modulesPath}/virtualisation/amazon-image.nix" ];
  ec2.hvm = true;
  networking.hostName = "mastiff";
  system.stateVersion = "22.05";

  environment = {
    systemPackages = with pkgs; [
      wget
      vim
      git
      tmux
      htop
    ];
  };

  services.caddy = {
    enable = true;
    email = "luiz@sourmash.bio";
    virtualHosts."mastiff.sourmash.bio".extraConfig = ''
      reverse_proxy http://127.0.0.1:3059
    '';
  };

  services.datadog-agent = {
    enable = true;
    enableLiveProcessCollection = true;
    enableTraceAgent = true;
    tags = [ "mastiff" ];
    apiKeyFile = "/var/log/datadog/ddagent.key";
    extraConfig = {
      logs_enabled = true;
    };
    checks = {
      "journal" = {
        logs = {
          type = "journald";
        };
      };
      "caddy" = {
        logs = {
          type = "file";
          path = "/var/log/caddy/access-mastiff.sourmash.bio.log";
          service = "mastiff";
          source = "caddy";
        };
      };
    };
  };
  users.users.datadog.extraGroups = ["systemd-journal"];

  mastiff.services.api.enable = true;

  networking.firewall = {
    enable = true;
    interfaces.ens5 = {
      allowedTCPPorts = [ 80 443 ];
    };
  };
}
