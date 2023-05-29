import "reflect-metadata"

import { DataSource, DataSourceOptions } from "typeorm";
import { User } from "./models/user.entity";

export const dataSourceOptions: DataSourceOptions = {
    type: 'postgres',
    host: 'db',
    port: 5432,
    username: 'postgres',
    password: 'budgeter',
    database: 'budgeter',
    entities: [User,],
    migrations: ["build/migrations/*.js"],
    synchronize: true,
}

const dataSource = new DataSource(dataSourceOptions)
export default dataSource