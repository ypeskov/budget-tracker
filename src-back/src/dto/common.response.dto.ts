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

    if (obj.code) {
      err.statusCode = obj.code;
    } else if (obj.status) {
      err.statusCode = obj.status;
    } else if (obj.response.statusCode) {
      err.statusCode = obj.response.statusCode;
    } 
    else {
      err.statusCode = HttpStatus.INTERNAL_SERVER_ERROR;
    }

    if (obj.message) {
      err.message = obj.message;
    } else if (obj.response.message) {
      err.message = obj.response.message;
    } else {
      err.message = 'Unknown error';
    }

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