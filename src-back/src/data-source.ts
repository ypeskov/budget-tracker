import "reflect-metadata"

import { DataSource, DataSourceOptions } from "typeorm";
import { User } from "./models/User.entity";
import { Currency } from "./models/Currency.entity";
import { Account } from "./models/Account.entity";
import { AccountType } from "./models/AccountType.entity";
import { UserCategory } from "./models/UserCategory.entity";
import { DefaultCategory } from "./models/DefaultCategory.entity";
import { Transaction } from "src/models/Transaction.entity";

export const dataSourceOptions: DataSourceOptions = {
    type: 'postgres',
    host: 'db',
    port: 5432,
    username: 'postgres',
    password: 'budgeter',
    database: 'budgeter',
    entities: [User, 
        Currency, 
        Account, 
        AccountType, 
        UserCategory, 
        Transaction,
        DefaultCategory],
    migrations: ["build/migrations/*.js"],
    synchronize: true,
}

const dataSource = new DataSource(dataSourceOptions)
export default dataSource