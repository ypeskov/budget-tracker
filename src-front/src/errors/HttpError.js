export class HttpError extends Error {
  /** string */
  statusCode;
  
  constructor(message, statusCode=500) {
    super(message);
    this.statusCode = statusCode;
  }
}
