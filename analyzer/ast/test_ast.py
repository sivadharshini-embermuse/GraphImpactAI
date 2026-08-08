from analyzer.ast.python_parser import parse_python
from analyzer.ast.javascript_parser import parse_javascript
from analyzer.ast.typescript_parser import parse_typescript
from analyzer.ast.java_parser import parse_java


def main():

    python_code = """
        import os

        class UserService:

            def get_user(self):
                return "Sivu"

        def calculate_price():
            return 100
        """

    javascript_code = """
        import React from "react";

        class App {
            render() {
                return "Hello";
            }
        }

        function calculatePrice() {
            return 100;
        }
        """

    typescript_code = """
        import React from "react";

        interface User {
            name: string;
        }

        class UserService {
            getUser(): string {
                return "Sivu";
            }
        }

        function calculatePrice(price: number): number {
            return price + 10;
        }
        """



    java_code = """
        import java.util.List;

        public class UserService {

            public String getUser() {
                return "Sivu";
            }

            public int calculatePrice(int price) {
                return price + 10;
            }
        }
        """

    python_result = parse_python(
        python_code
    )

    javascript_result = parse_javascript(
        javascript_code
    )

    typescript_result = parse_typescript(
        typescript_code
    )
    java_result = parse_java(java_code)




    print("\n========== PYTHON AST ==========")
    print(python_result)

    print("\n========== JAVASCRIPT AST ==========")
    print(javascript_result)

    print("\n========== TYPESCRIPT AST ==========")
    print(typescript_result)

    print("\n========== JAVA AST ==========")
    print(java_result)

    


if __name__ == "__main__":
    main()