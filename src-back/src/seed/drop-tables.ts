import dataSource from '../data-source';

async function dropTable() {  
  await dataSource.initialize();

  await dataSource.query('DROP TABLE transactions CASCADE');
  await dataSource.query('DROP TABLE users CASCADE');
  await dataSource.query('DROP TABLE accounts CASCADE');
  await dataSource.query('DROP TABLE account_types CASCADE');
  await dataSource.query('DROP TABLE default_categories CASCADE');
  await dataSource.query('DROP TABLE user_categories CASCADE');
  await dataSource.query('DROP TABLE currencies CASCADE');
  
  await dataSource.destroy();
}

dropTable().catch(console.error);