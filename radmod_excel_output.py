import exoplanetcatalogue as oec
import exoplanetcatalogue.astroquantities as aq
import quantities as pq
import csv

# Change databaseLocation to the path to the systems folder of the open exoplanet catalogue on your system
databaseLocation = '/Users/ryanv/Documents/git/open-exoplanet-catalogue-atmospheres/systems/'
oecDB = oec.OECDatabase(databaseLocation)

targets = oecDB.transitingPlanets

output = []

for planet in targets:

    star = planet.star

    try:
        output.append([
            star.name,
            float(star.M),  # need to float() to remove quantities unit information
            '{:.0f}'.format(float(star.T)),  # 0 decimal places
            float(star.R),
            float(planet.d),
            float(star.magK),
            '',  # seperator
            planet.name,
            float(planet.P),
            float(planet.T),
            float(planet.a.rescale(pq.m)),  # scale value from the catalogue standard of au to m
            float(planet.R.rescale(aq.R_e)),
            float(planet.albedo()),
            float(planet.M.rescale(aq.M_e)),
            float(planet.mu()),
        ])
    except Exception as error:  # report all failures (normally missing values) without crashing the script
        print planet.name, error

with open('radmod_targets.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(output)
