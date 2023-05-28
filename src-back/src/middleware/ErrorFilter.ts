import { ExceptionFilter, Catch, ArgumentsHost } from '@nestjs/common';
import { CommonResponse, ErrorResponse } from 'src/dto/common.response.dto';

@Catch()
export class ErrorFilter implements ExceptionFilter {
  catch(exception: any, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();

    let statusCode = 500;
    let message = 'Internal Server Error';

    if (typeof exception === 'object' && exception.statusCode !== undefined) {
      statusCode = exception.statusCode;
      message = exception.message || message;
    } else if (typeof exception === 'object' && exception.response.statusCode !== undefined) {
      statusCode = exception.response.statusCode;
      message = exception.response.message;
    } else if (exception instanceof Error) {
      message = exception.message || message;
    } 

    const errorResponse = new CommonResponse(false, ErrorResponse.createErrorFromObject(exception));

    response.status(statusCode).json(errorResponse);
  }
}
