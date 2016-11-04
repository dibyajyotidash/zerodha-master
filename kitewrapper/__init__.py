import json
from bs4 import BeautifulSoup
import requests
from kiteconnect import KiteConnect
import kiteconnect.exceptions as ex
USER_AGENT_STR = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
BASE_REFERER  = 'https://kite.zerodha.com/'
LOGIN_SUBMIT_URL = 'https://kite.zerodha.com/'


class KiteFront(KiteConnect):
    _login = "https://kite.zerodha.com"
    _api_root = "https://kite.zerodha.com/api"
    _root = _api_root
    _routes = {
        "parameters": "/parameters",
        "api.validate": "/session/token",
        "api.invalidate": "/session/token",
        "user.margins": "/margins/{segment}",
        
        "session" : "/session", #checked

        "orders": "/orders", #checked
        "trades": "/trades", #checked
        "orders.info": "/orders/{order_id}", #checked

        "orders.place": "/orders", #checked
        "orders.modify": "/orders/{variety}/{order_id}", 
        "orders.cancel": "/orders/{variety}/{order_id}",
        "orders.trades": "/orders/{order_id}/trades",

        "portfolio.positions": "/positions", #checked
        "portfolio.holdings": "/holdings", #checked
        "portfolio.positions.modify": "/positions",

        "market.instruments.all": "/instruments",
        "market.instruments": "/instruments/{exchange}",
        "market.quote": "/instruments/{exchange}/{tradingsymbol}",
        "market.historical": "/instruments/historical/{instrument_token}/{interval}",
        "market.trigger_range": "/instruments/{exchange}/{tradingsymbol}/trigger_range"
        }  
    
    def __init__(self, auth, *args, **kwargs):
        if not kwargs.get('api_key'):
            kwargs['api_key'] = 'kitefront'
        self._auth = auth
    
        self.session = requests.Session()
        self.headers_normal = {
                                'user-agent': USER_AGENT_STR,
                                'Host': 'kite.zerodha.com',
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                'Accept-Encoding': 'gzip, deflate, sdch',
                                'Referer': BASE_REFERER
                                }
        self.headers_json = {
                                'user-agent': USER_AGENT_STR,
                                'Host': 'kite.zerodha.com',
                                #'Accept': 'application/json, text/plain, */*',
                                #'Content-Type': 'application/json;charset=UTF-8',
                                'Accept': "*/*",
                                'Accept-Encoding' : 'gzip, deflate, sdch, br',
                                'Accept-Language': 'en-US,en;q=0.8',
                                'Cache-Control' : 'max-age=0',
                                'Connection': 'keep-alive',
                                #'Upgrade-Insecure-Requests':1
                             }
        super(KiteFront, self).__init__(*args, **kwargs)

    def connect(self):

        self._login_step1()

        params = self._qna(self.resp.text)
        return self._login_step2(params)


    def _login_step1(self):
        params = dict(user_id=self._auth['user_id'], password=self._auth['password'], login='')

        self.resp = self.session.post(LOGIN_SUBMIT_URL,
                                      proxies = self.proxies,
                                      data = params,
                                      headers = self.headers_normal,
                                      verify = False)
        return self.resp.text.find('Security') >=0


    def _qna(self,txt):
        params = dict()
        self.soup = BeautifulSoup(txt, 'html.parser')
        form = self.soup.find_all('form')[0]
        hidden_ips = form.find_all(attrs={'type': 'hidden'})
        for hidden_ip in hidden_ips:
            params[str(hidden_ip['name'])] = str(hidden_ip['value'])
        key = str(form.find_all('span')[0].contents[0])
        params['answer1'] = self._auth[key]
        key = str(form.find_all('span')[1].contents[0])
        params['answer2'] = self._auth[key]
        params['twofa'] = ''
        return params

    def _login_step2(self, params):
        self.resp = self.session.post(LOGIN_SUBMIT_URL,
                                      proxies = self.proxies,
                                      data = params,
                                      headers = self.headers_normal,
                                      verify = False)
        self.soup = BeautifulSoup(self.resp.text, 'html.parser')


        return self._check_step2()

    def _check_step2(self):
        return (self.resp.text.find('Positions')) >= 0   

    # orders
    def order_place(self,
                    exchange,
                    tradingsymbol,
                    transaction_type,
                    quantity,
                    order_type,
                    price=0,
                    product="CNC",
                    validity="DAY",
                    disclosed_quantity=0,
                    trigger_price=0,
                    squareoff_value=0,
                    stoploss_value=0,
                    trailing_stoploss=0,
                    variety="regular",
                    ):
        """Place an order."""
        params = locals()
        del(params["self"])
        return self._post("orders.place", params)["order_id"]

    def _request(self, route, method, parameters=None):
        """Make an HTTP request."""
        params = {}
        if parameters:
            params = parameters.copy()
        """
        # Micro cache?
        if self.micro_cache is False:
            params["no_micro_cache"] = 1

        # Is there a token?.
        if self.access_token:
            params["access_token"] = self.access_token

        # override instance's API key if one is supplied in the params
        if "api_key" not in params or not params.get("api_key"):
            params["api_key"] = self.api_key
        """
        uri = self._routes[route]

        # 'RESTful' URLs.
        if "{" in uri:
            for k in params:
                uri = uri.replace("{" + k + "}", str(params[k]))
        if uri.find('https') >= 0:
            url = uri
        else:
            url = self._root + uri


        try:
            if self.debug:
                print(method)
                print(url)
                print(params if method == "POST" else None)
                print(params if method != "POST" else None)
            r = self.session.request(method,
                    url,
                    json=params if method == "POST" else None,
                    params=params if method != "POST" else None,
                    headers=self.headers_json,
                    verify=False,
                    allow_redirects=True,
                    timeout=self._timeout,
                    proxies=self.proxies)
            self.r = r
            if self.debug:
                import pdb; pdb.set_trace()
        except requests.ConnectionError:
            raise ex.ClientNetworkException("Gateway connection error", code=503)
        except requests.Timeout:
            raise ex.ClientNetworkException("Gateway timed out", code=504)
        except requests.HTTPError:
            raise ex.ClientNetworkException("Invalid response from gateway", code=502)
        except Exception as e:
            raise ex.ClientNetworkException(e.message, code=500)


        # Validate the content type.
        if "json" in r.headers["content-type"]:
            try:
                data = json.loads(r.content.decode('utf8'))
            except:
                raise ex.DataException("Couldn't parse JSON response")

            # api error
            if data["status"] == "error":
                if r.status_code == 403:
                    if self.session_hook:
                        self.session_hook()
                        return

                # native Kite errors
                exp = getattr(ex, data["error_type"])
                if data["error_type"] == "TwoFAException":
                    raise(ex.TwoFAException(data["message"],
                                            questions=data["questions"] if "questions" in data else [],
                                            code=r.status_code))
                elif exp:
                    raise(exp(data["message"], code=r.status_code))
                else:
                    raise(ex.GeneralException(data["message"], code=r.status_code))

            return data["data"]
        elif "csv" in r.headers["content-type"]:
            return r.content
        else:
            raise ex.DataException("Unknown Content-Type (%s) in response: (%s)" % (r.headers["content-type"], r.content))

