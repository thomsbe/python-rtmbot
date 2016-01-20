from fhem import get_fhem, set_fhem

print get_fhem('max.t_office_thorsten')['Readings']['temperature']['Value']

set_fhem('set MaxOffice desiredTemperature auto 18')