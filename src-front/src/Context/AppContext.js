import React, {useState} from 'react';

const UserContext = React.createContext();

const AppProvider = ({children}) => {
  const userInit = {
    id: 1,
    email: 'user1@example.com',
    firstName: 'Yura',
    lastName: 'Peskov',
    isLoggedIn: false,
  };

  const [user, setUser] = useState(userInit);
  const updateUser = () => {console.log('Update user is called')}

  return (
    <UserContext.Provider value={{user, updateUser}}>
      {children}
    </UserContext.Provider>
  );
};

export {AppProvider, UserContext};