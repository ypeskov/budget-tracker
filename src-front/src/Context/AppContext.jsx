import React, {useState} from 'react';

const UserContext = React.createContext();

const defaultUserInfo = {
  id: null,
  email: '',
  firstName: '',
  lastName: '',
};

const AppProvider = ({children}) => {
  const userInit = {
    ...defaultUserInfo,
    isLoggedIn: false,
  };

  const [user, setUser] = useState(userInit);

  const updateUser = (userData) => {
    let tmp = {};
    if (userData.isLoggedIn) { tmp.isLoggedIn = userData.isLoggedIn; }
    if (userData.accessToken) { tmp.accessToken = userData.accessToken; }
    if (userData.email) { tmp.email = userData.email; }
    if (userData.firstName) { tmp.firstName = userData.firstName; }
    if (userData.lastName) { tmp.lastName = userData.lastName; }
    if (userData.id) { tmp.id = userData.id; }

    setUser(prevUser => {
      return  {
        ...prevUser,
        ...tmp,
      }
    });
  }

  return (
    <UserContext.Provider value={{user, updateUser}}>
      {children}
    </UserContext.Provider>
  );
};

export {AppProvider, UserContext};