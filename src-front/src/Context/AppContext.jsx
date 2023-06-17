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
    userInfo: defaultUserInfo,
    isLoggedIn: false,
  };

  const [user, setUser] = useState(userInit);
  const updateUser = (userData) => {
    console.log(userData)
    setUser(prevUser => ({
      ...prevUser,
      userInfo: userData,
    }));
  }

  return (
    <UserContext.Provider value={{user, updateUser}}>
      {children}
    </UserContext.Provider>
  );
};

export {AppProvider, UserContext};