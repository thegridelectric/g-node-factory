from gnf.schemata import OptinTadeedAlgo
from gnf.schemata import OptinTadeedAlgo_Maker as Maker


d = {
    "TaDaemonAddr": "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA",
    "TaOwnerAddr": "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI",
    "ValidatorAddr": "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII",
    "NewDeedOptInMtx": "gqRtc2lng6ZzdWJzaWeTgqJwa8Qgi1hzb1WaDzF+215cR8xmiRfUQMrnjqHtQV5PiFBAUtmhc8RAPGWsPRqzCnTQx1xN+3tvigaC1C/zxcOrOOqUVTkTNfPAV4E10Cx07Ypk21sd+rSiDaOGcnGTK6VpLQisOC0KAoGicGvEIG5vSU8gE+qQnjKSeqJtNHiRNXX6dwpPfbh94jqJIPZvgaJwa8QgVc0/JRFMI8MKUvc+penSkoOdllhI0XSQwC/nlbeJLwajdGhyAqF2AaN0eG6JpGFyY3bEIBDvhZHURmM5X1LtflwM7F7VLzofXv8vUEFnwWeRv4xfo2ZlZc0D6KJmdiijZ2VuqnNhbmRuZXQtdjGiZ2jEIC/iF+bI4LU6UTgG4SIxyD10PS0/vNAEa93OC5SVRFn6omx2zQQQo3NuZMQgEO+FkdRGYzlfUu1+XAzsXtUvOh9e/y9QQWfBZ5G/jF+kdHlwZaVheGZlcqR4YWlkDQ==",
    "TypeName": "optin.tadeed.algo",
    "Version": "000",
}

optin = Maker.dict_to_tuple(d)
