#!/usr/bin/env python3
# -*- coding: utf-8 -*-


""" git-passport is a Git command and hook written in Python to manage multiple
    Git users / user identities.
"""

if __name__ == "__main__":
    import os.path
    import sys

    from passport import (
        arg,
        case,
        configuration,
        dialog,
        git
    )

    args = arg.release()
    config_file = os.path.expanduser("~/.gitpassport")

    if (
        not configuration.preset(config_file) or
        not configuration.validate_scheme(config_file) or
        not configuration.validate_values(config_file) or
        not git.is_infected()
    ):
        sys.exit(1)
    else:
        config = configuration.release(config_file)

    if config["enable_hook"]:
        local_email = git.get_config("local", "email")
        local_name = git.get_config("local", "name")
        local_signingkey = git.get_config("local", "signingkey")
        local_url = git.get_config("local", "url")

        if args.select:
            local_name = None
            local_email = None
            local_signingkey = None
            local_url = 'select-from-all-passports'
            git.remove_config(verbose=False)

        if args.delete:
            git.remove_config()
            sys.exit(0)

        if args.active:
            case.active_identity(
                config,
                local_email,
                local_name,
                local_url,
                signingkey=local_signingkey,
                style="compact",
            )
            sys.exit(0)

        if args.passports:
            dialog.print_choices(config["git_passports"])
            exit(0)

        if local_email and local_name:
            case.active_identity(
                config,
                local_email,
                local_name,
                local_url,
                signingkey=local_signingkey,
            )
            sys.exit(0)

        if local_url:
            candidates = case.url_exists(config, local_url)
        else:
            candidates = case.no_url_exists(config)

        selected_id = dialog.get_input(candidates.keys())
        if selected_id is not None:
            git.set_config(candidates[selected_id]["email"], "email")
            git.set_config(candidates[selected_id]["name"], "name")
            signingkey = candidates[selected_id].get("signingkey")
            if signingkey:
                git.set_config(signingkey, "signingkey")
            sys.exit(0)
    else:
        print("git-passport is currently disabled.")
        sys.exit(0)
