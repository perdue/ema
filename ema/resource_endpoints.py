def _build_resource(base, view, resource, action):
    l = [base, view, resource, action]
    delimiter = '/'
    return delimiter.join(l)


BASE = 'aps-api-web/api/view'

#resources = {
#    'users': 'users',
#    'system': 'system',
#    'ecu': 'ecu',
#    'module': 'module'
#}

#user_endpoints = {
#    'authorize': _build_resource(BASE, VER, resources['users'], 'authorize'),
#    'login': _build_resource(BASE, VER, resources['users'], 'loginAndGetViewList'),
#    'info': _build_resource(BASE, VER, resources['users'], 'getUserInfo')
#}

#system_endpoints = {
#    'power': _build_resource(BASE, VER, resources['system'], 'getPowerInfo')
#}

#ecu_endpoints = {
#    'power': _build_resource(BASE, VER, resources['ecu'], 'getPowerInfo')
#}

#module_endpoints = {
#    'views': _build_resource(BASE, VER, resources['module'], 'getViewListBySystemId'),
#    'detail': _build_resource(BASE, VER, resources['module'], 'getViewDetailByView'),
#    'power': _build_resource(BASE, VER, resources['module'], 'getUIDPowerByView')
#}

reg_endpoints = {
    'checkUser': _build_resource(BASE, 'registration', 'user', 'checkUser'),
      'ecuInfo': _build_resource(BASE, 'registration', 'ecu', 'getEcuInfoBelowUser')
}

check_codes = {
    'checkUser': 'AFF2B9F8B513D91AE48968A2A529BFF3BA6FF9E9',
      'ecuInfo': '9E70A86F59E8EF120C13470327CE62100DCE072C'
}

def build_url(host, port, endpoint):
    url = 'http://' + \
          host + ':' + str(port) + \
          '/' + endpoint
    #print(url)
    return url

def check_endpoints(host, port):
#    _print_eps(host, port, user_endpoints)
#    _print_eps(host, port, system_endpoints)
#    _print_eps(host, port, ecu_endpoints)
#    _print_eps(host, port, module_endpoints)
    _print_eps(host, port, reg_endpoints)

def _print_eps(host, port, endpoints):
    for ep in endpoints.values():
      print(build_url(host, port, ep))
