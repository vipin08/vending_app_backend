## Vending Frontend

Frontend is build on Reactjs and Redux for better state management.

### Folder Structure:

```
.
├── README.md
├── node_modules
├── static
│   ├── index.html
│   └── js
│       └── src
│           ├── actions
│           │   └── index.js
│           ├── components
│           │   ├── ProductListItem.js
│           │   └── PurchasedProductListItem.js
│           ├── constants
│           │   └── ActionTypes.js
│           ├── containers
│           │   ├── App.js
│           │   ├── BalancePanel.js
│           │   ├── BanknotePanel.js
│           │   ├── ProductList.js
│           │   ├── PurchasedProductList.js
│           │   └── Sidebar.js
│           ├── index.js
│           └── reducers
│               ├── balance.js
│               ├── index.js
│               ├── products.js
│               └── purchasedProducts.js
└── webpack.config.js
├── package-lock.json
├── package.json
├── static
│   ├── index.html
│   └── js
│       └── src
└── webpack.config.js
```
#### Frontend URL:
```url
https//:localhost:8080
```

### Pending on frontend:
1. Handling refund behaviour.
2. End User Login.
3. User cart

### Tech stack

- React - because it works very effectively with DOM.
- Redux - because it's great state manager with its reducers and unidirectional data flow.
- Redux Thunk - allows to manage async actions.
- ES2015 - to write less code and use modern features.
- Webpack - to watch, lint, transpile and bundle modules.
- Bootstrap - to build simple responsive UI very fast.

#### Functionality:

1. I decided to use just Rupee banknotes of ₹10, ₹20, ₹50, ₹100 and set prices on reactjs as int numbers on `Sidebar.js`.
2. Also I've added number of products so the product could be out of stock when count is `0` from project list api.
3. All purchased product shown on right side after cick on buy button.
4. Refund only eligible if `is_refundable` is `true` in product listing API.






