import { createConnection } from 'typeorm';
import { dataSourceOptions } from '../data-source';
import { DefaultCategory } from '../models/DefaultCategory.entity';

export async function loadDefaultCategories() {
  try {
    const connection = await createConnection(dataSourceOptions);
    const categoryRepository = connection.getRepository(DefaultCategory);

    const template: any = {
      parent_id: null,
      is_income: undefined,
      is_deleted: undefined,
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
      { id: 11, name: 'Parking', ...template },
      { id: 16, name: 'Salary', ...template },
      { id: 17, name: 'Deposit', ...template },
      { id: 18, name: 'Present', ...template },
      { id: 19, name: 'Rent', ...template },
      { id: 20, name: 'Social', ...template },
      { id: 21, name: 'Other', ...template },
    ];

    try {
      await categoryRepository.save(defaultValues);

      const parentAutomobile = await DefaultCategory.findOneByOrFail({name: 'Automobile'});
      defaultValues = [
        { id: 12, name: 'Fuel', parent: parentAutomobile, ...template },
        { id: 13, name: 'Service', parent: parentAutomobile, ...template },
      ];
      await categoryRepository.save(defaultValues);

      const transportAutomobile = await DefaultCategory.findOneByOrFail({name: 'Transport'});
      defaultValues = [
        { id: 14, name: 'Taxi', parent: transportAutomobile, ...template },
        { id: 15, name: 'Food', parent: transportAutomobile, ...template },
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
