def _build_resource(base, view, resource, action):
    l = [base, view, resource, action]
    delimiter = '/'
    return delimiter.join(l)

BASE = 'aps-api-web/api/view'

reg_endpoints = {
     'checkUser': _build_resource(BASE, 'registration', 'user', 'checkUser'),
       'ecuInfo': _build_resource(BASE, 'registration', 'ecu', 'getEcuInfoBelowUser'),
      'viewList': _build_resource(BASE, 'registration', 'view', 'getViewListBelowUser'),
    'viewDetail': _build_resource(BASE, 'registration', 'view', 'getViewDetailsOfManualView')
}

prod_endpoints = {
    'powerBatch': _build_resource(BASE, 'production', 'dc', 'getPowerOnCurrentDayInBatch')
}

def build_url(host, port, endpoint):
    url = 'http://' + \
          host + ':' + str(port) + \
          '/' + endpoint
    return url

def check_endpoints(host, port):
    _print_eps(host, port, reg_endpoints)
    _print_eps(host, port, prod_endpoints)

def _print_eps(host, port, endpoints):
    for ep in endpoints.values():
      print(build_url(host, port, ep))
