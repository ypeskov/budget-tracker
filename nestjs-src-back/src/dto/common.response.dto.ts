import { HttpStatus } from "@nestjs/common";

export class ErrorResponse {
  public statusCode: number

  public message: string

  public meta: string | undefined

  constructor(code: number=500, msg: string='', meta='') {
    this.statusCode = code;
    this.message = msg;
    this.meta = meta;
  }

  static createErrorFromObject(obj: object | any): ErrorResponse {
    let err = new ErrorResponse();

    err.statusCode = obj?.code 
      || obj?.response?.statusCode 
      || obj?.statusCode 
      || HttpStatus.INTERNAL_SERVER_ERROR;

    err.message = obj?.response?.message 
      || obj?.message 
      || 'Unknown error';

    return err;
  }
}

export class CommonResponse {
  success: boolean

  payload: object | ErrorResponse

  constructor(success: boolean, payload: object | ErrorResponse) {
    this.success = success;
    this.payload = payload;
  }
}