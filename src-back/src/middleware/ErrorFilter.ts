import { ExceptionFilter, Catch, ArgumentsHost } from '@nestjs/common';
import { CommonResponse, ErrorResponse } from 'src/dto/common.response.dto';

@Catch()
export class ErrorFilter implements ExceptionFilter {
  catch(exception: any, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();

    let statusCode = 500;
    let message = 'Internal Server Error';

    statusCode = exception?.response?.statusCode 
      || exception?.status 
      || statusCode;
    message = exception?.response?.message 
      || exception?.message 
      || message;

    const errorResponse = new CommonResponse(false, ErrorResponse.createErrorFromObject(exception));

    response.status(statusCode).json(errorResponse);
  }
}
