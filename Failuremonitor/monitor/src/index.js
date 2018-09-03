import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
/*
const products = [{
  name: "onion",
  price: ".99",
  id: 1
}, {
  name: "pepper",
  price: "1.25",
  id: 2
}, {
  name: "broccoli",
  price: "3.00",
  id: 3
}];
const TableRow = ({row}) => (
  <tr>
    <td key={row.name}>{row.name}</td>
    <td key={row.id}>{row.id}</td>
    <td key={row.price}>{row.price}</td>
  </tr>
);

const Table = ({data}) = (
  <table>
    {data.map(row => {
      <TableRow row={row} />
    })}
  </table>
);

ReactDOM.render(
  <Table data={products} />,
  document.getElementById("root")
);
*/
ReactDOM.render(<App />, document.getElementById('root'));

registerServiceWorker();
