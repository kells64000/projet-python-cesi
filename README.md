# projet-python-cesi

## Station météo sur raspberry

### Versionning

Pour ce projet nous utilisons git flow

### Database

La base de donnée est mysql

```bash
user: pi
mdp: python2019
database: station-meteo

mysql -u pi -ppython2019 -D station-meteo
```

Pour Creer la bdd  :

```bash
mysql -u pi -ppython2019 -D station-meteo < db/database.sql
```

Notre Capteur est le 2