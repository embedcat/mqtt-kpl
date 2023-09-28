```
cp mqtt-kpl.service ~/.config/systemd/user/
systemctl --user list-unit-files | grep mqtt-kpl
systemctl --user daemon-reload
systemctl --user start mqtt-kpl.service
```

logs:
```
journalctl --user-unit mqtt-kpl.service -n100
```