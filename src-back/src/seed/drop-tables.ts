import dataSource from '../data-source';

async function dropTable() {  
  await dataSource.initialize();

  await dataSource.query('DROP TABLE accounts');
  await dataSource.query('DROP TABLE account_types');
  await dataSource.query('DROP TABLE default_categories');
  await dataSource.query('DROP TABLE user_categories');
  await dataSource.query('DROP TABLE users');
  await dataSource.query('DROP TABLE currencies');
  
  await dataSource.destroy();
}

dropTable().catch(console.error);