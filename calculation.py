import grpc
from concurrent import futures
import sympy as sp
import calculation_pb2
import calculation_pb2_grpc
import logging
from sympy.parsing.sympy_parser import parse_expr

class CalculatorService(calculation_pb2_grpc.CalculatorServiceServicer):

    def Calculate(self, request, context):
        calc_type = request.calculation_type.upper()  # Normalize
        if calc_type == "LATEX":
            return self.calculate_latex(request)
        elif calc_type == "RESULT":
            return self.calculate_result(request)
        else:
            return calculation_pb2.CalculationResponse(
                response_code="error",
                response_msg=f"Unknown calculation_type: {request.calculation_type}"
            )

    def parse_expression(self, expr_string, parameters):
        """Helper to parse an expression with given parameters."""
        subs = {p.name: p.value for p in parameters}
        symbols = {name: sp.symbols(name) for name in subs.keys()}
        expr = parse_expr(expr_string, local_dict=symbols)
        return expr, subs

    def calculate_latex(self, request):
        expr_string = request.expression

        try:
            expr, _ = self.parse_expression(expr_string, request.parameters)
            factored = sp.factor(expr)
            latex_code = sp.latex(factored)

            return calculation_pb2.CalculationResponse(
                response_code="ok",
                response_msg="Success",
                latex=latex_code
            )
        except Exception as e:
            return calculation_pb2.CalculationResponse(
                response_code="error",
                response_msg=str(e)
            )

    def calculate_result(self, request):
        expr_string = request.expression

        try:
            expr, subs = self.parse_expression(expr_string, request.parameters)
            factored_expr = sp.factor(expr)

            # Substitute parameters
            substituted_expr = factored_expr.subs(subs)

            # Evaluate the result
            result = substituted_expr.evalf()

            return calculation_pb2.CalculationResponse(
                response_code="ok",
                response_msg="Success",
                result=float(result)
            )
        except Exception as e:
            return calculation_pb2.CalculationResponse(
                response_code="error",
                response_msg=str(e)
            )


        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculation_pb2_grpc.add_CalculatorServiceServicer_to_server(CalculatorService(),server)
    server.add_insecure_port('[::]:8888')
    server.start()
    print("Server started on port 8888...")
    server.wait_for_termination()
    
if __name__ == '__main__':
    logging.basicConfig()
    serve()
    
         