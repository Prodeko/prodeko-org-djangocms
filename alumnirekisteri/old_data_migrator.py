import numpy as np
#from rekisteri.models import *
#from auth2.models import *

# Bring in data
users = np.loadtxt('old_data_files/users_taulu.csv', delimiter=';', dtype='str')
perus = np.loadtxt('old_data_files/perus_taulu.csv', delimiter=';', dtype='str')
akatkunn = np.loadtxt('old_data_files/akatkunn_taulu.csv', delimiter=';', dtype='str')
lapset = np.loadtxt('old_data_files/lapset_taulu.csv', delimiter=';', dtype='str')
edelt_op = np.loadtxt('old_data_files/edelt-op_taulu.csv', delimiter=';', dtype='str')
jatko_op = np.loadtxt('old_data_files/jatko-op_taulu.csv', delimiter=';', dtype='str')
jarjestotoim = np.loadtxt('old_data_files/jarjestotoim_taulu.csv', delimiter=';', dtype='str')
luottamusteht = np.loadtxt('old_data_files/luottamusteht_taulu.csv', delimiter=';', dtype='str')
puolisot = np.loadtxt('old_data_files/puolisot_taulu.csv', delimiter=';', dtype='str')
sivutoimet = np.loadtxt('old_data_files/sivutoimet_taulu.csv', delimiter=';', dtype='str')
tekniset_op = np.loadtxt('old_data_files/tekniset-op_taulu.csv', delimiter=';', dtype='str')
vanhatyo = np.genfromtxt('old_data_files/vanhatyo_taulu.csv', delimiter=';', dtype='str')
vuorilinj = np.loadtxt('old_data_files/vuorilinj_taulu.csv', delimiter=';', dtype='str')
yo_kunn = np.genfromtxt('old_data_files/yo_kunnianosoitukset_taulu.csv', delimiter=';', dtype='str')

print(users[0])

# Tee tähän dict noista tauluista, joista pitää id:llä hakea tavarat
perus_dict = 0

# Create objects without headers, update variable to contain just the data rows
users_data = np.delete(users, (0), axis=0)
perus_data = np.delete(perus, (0), axis=0)
akatkunn_data = np.delete(akatkunn, (0), axis=0)
lapset_data = np.delete(lapset, (0), axis=0)
edelt_op_data = np.delete(edelt_op, (0), axis=0)
jatko_op_data = np.delete(jatko_op, (0), axis=0)
jarjestotoim_data = np.delete(jarjestotoim, (0), axis=0)
luottamusteht_data = np.delete(luottamusteht, (0), axis=0)
puolisot_data = np.delete(puolisot, (0), axis=0)
sivutoimet_data = np.delete(sivutoimet, (0), axis=0)
tekniset_op_data = np.delete(tekniset_op, (0), axis=0)
vanhatyo_data = np.delete(vanhatyo, (0), axis=0)
vuorilinj_data = np.delete(vuorilinj, (0), axis=0)
yo_kunn_data = np.delete(yo_kunn, (0), axis=0)

#print(users[:5])

'''
for useri in users:
    perus_object =
    u = User(email=useri[3], )
    #do shiz
    #save da shiz
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
'''
