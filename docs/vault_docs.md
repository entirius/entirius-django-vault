# Vault API

## GET card list for payment method
Requires user authentication and the X-API-KEY header.
Returns the card list for the given payment method.

`GET http://127.0.0.1:3301/api/vault/V1/test-channel-pl/payment_card/<payment_method>/`:
```json
{
    "meta": {
        "status": "OK",
        "message": "",
        "messages": [],
        "regional": {
            "language": null,
            "currency": null,
            "country": null
        }
    },
    "data": [
        {
            "value": "TOKC_7ZAZ4JH4FJSTQSZYI8NJDAVEPE3",
            "brandImageUrl": "https://static.payu.com/images/mobile/visa.png",
            "status": "ACTIVE",
            "cardExpirationYear": 2029,
            "cardExpirationMonth": 12,
            "cardNumberMasked": "444433******1111",
            "cardScheme": "VS",
            "cardBrand": "VISA"
        }
    ]
}


```
Example
`http://127.0.0.1:3301/api/vault/V1/test-channel-pl/payment_card/payu_card/`

## GET card list for all payment method available
Requires user authentication and the X-API-KEY header.
Returns the card list for all payment methods.

`GET http://127.0.0.1:3301/api/vault/V1/test-channel-pl/payment_card/`:
```json
{
    "meta": {
        "status": "OK",
        "message": "",
        "messages": [],
        "regional": {
            "language": null,
            "currency": null,
            "country": null
        }
    },
    "data": [
        {
            "value": "TOKC_7ZAZ4JH4FJSTQSZYI8NJDAVEPE3",
            "brandImageUrl": "https://static.payu.com/images/mobile/visa.png",
            "status": "ACTIVE",
            "cardExpirationYear": 2029,
            "cardExpirationMonth": 12,
            "cardNumberMasked": "444433******1111",
            "cardScheme": "VS",
            "cardBrand": "VISA"
        }
    ]
}


```
Example
`http://127.0.0.1:3301/api/vault/V1/test-channel-pl/payment_card/`

## POST add card for payment method
Requires user authentication and the X-API-KEY header.
Adds a card for the given payment method. Pass the card token in the body.

`POST http://127.0.0.1:3301/api/vault/V1/test-channel-pl/payment_card/<payment_method>/`:
Body:
```json
{
    "value": "TOK_7ZAZ4JH4FJSTQSZYI8NJDAVEPE3"
}
```
Response:
```json
{
    "meta": {
        "status": "OK",
        "message": "",
        "messages": [],
        "regional": {
            "language": null,
            "currency": null,
            "country": null
        }
    },
    "data": {
        "status": "success"
    }
}
```
Example
`POST http://127.0.0.1:3301/api/vault/V1/test-channel-pl/payment_card/payu_card/`
+ body:
```json
{
    "value": "TOKC_7ZAZ4JH4FJSTQSZYI8NJDAVEPE3"
}
```


## DELETE - delete card for payment method
Requires user authentication and the X-API-KEY header.
Deletes a card for the given payment method. Pass the card token in the body.

`DELETE http://127.0.0.1:3301/api/vault/V1/test-channel-pl/payment_card/<payment_method>/`:
Body:
```json
{
    "value": "TOKC_7ZAZ4JH4FJSTQSZYI8NJDAVEPE3"
}
```
Response:
```json
{
    "meta": {
        "status": "OK",
        "message": "",
        "messages": [],
        "regional": {
            "language": null,
            "currency": null,
            "country": null
        }
    },
    "data": {
        "status": "success"
    }
}
```
Example
`DELETE http://127.0.0.1:3301/api/vault/V1/test-channel-pl/payment_card/payu_card/`
+ body:
```json
{
    "value": "TOKC_7ZAZ4JH4FJSTQSZYI8NJDAVEPE3"
}
```