import { IsNotEmpty, IsNumber, IsString } from "class-validator"

export class CreateTransactionDTO {
    @IsString()
    short_description?: string

    @IsString()
    long_description?: string

    @IsNotEmpty()
    @IsNumber()
    amount: number

    @IsNotEmpty()
    @IsNumber()
    category_id: number

    @IsNotEmpty()
    @IsNumber()
    currency_id: number

    @IsNotEmpty()
    @IsNumber()
    account_id: number
}