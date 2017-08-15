# pevy

![pevy](extra/pevy.png?raw=true)

## Development with virtualenv

```bash
virtualenv env
source env/bin/activate
python setup.py install
pevy -c pevy.yaml
```

## Deployment using systemd

```bash
./install.sh
systemctl status pevy
tail -f pevy.log
```
