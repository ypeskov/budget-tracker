import { IsNotEmpty, IsEmail, IsString } from "class-validator"

export class CreateUserDTO {
    @IsString()
    firstName: string

    @IsString()
    lastName: string

    @IsNotEmpty()
    password: string

    @IsEmail()
    email: string
}