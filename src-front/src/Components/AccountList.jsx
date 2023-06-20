import { useContext, useEffect, useState, useRef } from 'react';
import { UserContext } from '../Context/AppContext';

import './AccountList.css';

const apiDomain = `${process.env.REACT_APP_API_URL}`;

export default function AccountList() {
  const { user } = useContext(UserContext);
  const [accs, setAccs] = useState([]);
  const isRequestCompletedRef = useRef(false);

  useEffect(() => {
    if (!isRequestCompletedRef.current) {
      async function getMyAccoutns() {
        isRequestCompletedRef.current = true;
        const response = await fetch(`${apiDomain}/accounts`, {
          headers: {
            "auth-token": user.accessToken
          },
        });
  
        const data = await response.json();
        setAccs(data);
      }
  
      getMyAccoutns();
    }
  }, [user.accessToken]);

  const accsJSX = accs.map(acc => (
    <div key={acc.id} className='account-container'>
      <div>Name: {acc.name}</div>
      <div>Balance: {acc.balance}</div>
    </div>
  ));

  return (
    <>
      {accsJSX}
    </>
  );
}
