import { IsDate, IsDateString, IsNotEmpty, IsNumber, IsOptional, IsString } from "class-validator"

export class CreateAccountDTO {
  @IsNotEmpty()  
  @IsString()
  name: string

  @IsNotEmpty()
  @IsNumber()
  accountTypeId: number

  @IsNotEmpty()
  @IsNumber()
  userId: number

  @IsNotEmpty()
  @IsNumber()
  currencyId: number

  @IsNumber()
  @IsOptional()
  initialBalance: number

  @IsDateString()
  @IsOptional()
  openingDate: Date

  @IsNumber()
  @IsOptional()
  opening_exchane_rate: number

  @IsString()
  @IsOptional()
  comment: string
}