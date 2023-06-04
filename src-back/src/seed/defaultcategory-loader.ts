import { createConnection } from 'typeorm';
import { dataSourceOptions } from '../data-source';
import { DefaultCategory } from '../models/DefaultCategory.entity';

export async function loadDefaultCategories() {
  try {
    const connection = await createConnection(dataSourceOptions);
    const categoryRepository = connection.getRepository(DefaultCategory);

    const template: any = {
      parent_id: null,
      is_income: false,
      is_deleted: false,
      created_at: new Date(),
      updated_at: new Date(),
    };

    let defaultValues: DefaultCategory[] = [
      { id: 1, name: 'Life', ...template},
      { id: 2, name: 'Food', ...template },
      { id: 3, name: 'Automobile', ...template},
      { id: 4, name: 'Transport', ...template},
      { id: 5, name: 'Housing', ...template},
      { id: 6, name: 'Health', ...template},
      { id: 7, name: 'Education', ...template},
      { id: 8, name: 'Entertainment', ...template},
      { id: 9, name: 'Finances', ...template},
      { id: 10, name: 'Other', ...template},
      
      { id: 16, name: 'Salary', ...template, is_income: true },
      { id: 17, name: 'Deposit', ...template, is_income: true },
      { id: 18, name: 'Present', ...template, is_income: true },
      { id: 19, name: 'Rent', ...template, is_income: true },
      { id: 20, name: 'Social', ...template, is_income: true },
      { id: 21, name: 'Other', ...template, is_income: true },
    ];

    try {
      await categoryRepository.save(defaultValues);

      const parentAutomobile = await DefaultCategory.findOneByOrFail({name: 'Automobile'});
      defaultValues = [
        { ...template, name: 'Parking', parent: parentAutomobile,},
        { ...template, name: 'Fuel', parent: parentAutomobile,},
        { ...template, name: 'Service', parent: parentAutomobile,},
      ];
      await categoryRepository.save(defaultValues);

      const transportAutomobile = await DefaultCategory.findOneByOrFail({name: 'Transport'});
      defaultValues = [
        { ...template, name: 'Taxi', parent: transportAutomobile, },
        { ...template, name: 'Airplane', parent: transportAutomobile, },
      ];
      await categoryRepository.save(defaultValues);

      console.log('Default categories are loaded in DB');
    } catch (error) {
      console.error(error);
    }

    await connection.destroy();
  } catch (error) {
    console.error('Error while loading currencies:', error);
  }
}

if (require.main === module) {
  loadDefaultCategories();
}