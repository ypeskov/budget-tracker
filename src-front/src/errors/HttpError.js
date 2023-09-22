export class HttpError extends Error {
  /** number */
  statusCode;
  
  constructor(message, statusCode=500) {
    super(message);
    this.statusCode = statusCode;
  }
}
