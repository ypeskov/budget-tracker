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

  const [user] = useState(userInit);
  const updateUser = () => {console.log('Update user is called')}

  return (
    <UserContext.Provider value={{user, updateUser}}>
      {children}
    </UserContext.Provider>
  );
};

export {AppProvider, UserContext};