def _build_resource(base, ver, resource, action):
    l = [base, ver, resource, action]
    delimiter = '/'
    return delimiter.join(l)


BASE = 'apsema'
VER  = 'v1'

resources = {
    'users': 'users',
    'system': 'system',
    'ecu': 'ecu',
    'module': 'module'
}

user_endpoints = {
    'authorize': _build_resource(BASE, VER, resources['users'], 'authorize'),
    'login': _build_resource(BASE, VER, resources['users'], 'loginAndGetViewList'),
    'info': _build_resource(BASE, VER, resources['users'], 'getUserInfo')
}

system_endpoints = {
    'power': _build_resource(BASE, VER, resources['system'], 'getPowerInfo')
}

ecu_endpoints = {
    'power': _build_resource(BASE, VER, resources['ecu'], 'getPowerInfo')
}

module_endpoints = {
    'views': _build_resource(BASE, VER, resources['module'], 'getViewListBySystemId'),
    'detail': _build_resource(BASE, VER, resources['module'], 'getViewDetailByView'),
    'power': _build_resource(BASE, VER, resources['module'], 'getUIDPowerByView')
}

#print(resources)
#print(user_endpoints)
#print(system_endpoints)
#print(ecu_endpoints)
#print(module_endpoints)
