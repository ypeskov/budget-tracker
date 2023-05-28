export class ErrorResponse {
  code: number

  message: string

  meta: string | undefined

  constructor(code: number, msg: string, meta='') {
    this.code = code;
    this.message = msg;
    this.meta = meta;
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