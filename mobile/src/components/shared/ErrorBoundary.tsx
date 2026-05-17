/** * Error Boundary
for graceful failure handling */ "use client";
import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
interface Props {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}
interface State {
  hasError: boolean;
  error?: Error;
}
export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
    };
  }
  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
    };
  }
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("ErrorBoundary caught:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="flex h-screen items-center justify-center p-4">
            {" "}
            <Card className="w-full max-w-md">
              {" "}
              <CardHeader>
                {" "}
                <CardTitle className="text-red-600">
                  Something went wrong
                </CardTitle>{" "}
              </CardHeader>{" "}
              <CardContent>
                {" "}
                <p className="text-sm text-slate-600 mb-4">
                  {" "}
                  {this.state.error?.message || "An unexpected error occurred"}
                </p>{" "}
                <Button
                  onClick={() =>
                    this.setState({
                      hasError: false,
                    })
                  }
                >
                  {" "}
                  Try Again{" "}
                </Button>{" "}
              </CardContent>{" "}
            </Card>{" "}
          </div>
        )
      );
    }
    return this.props.children;
  }
}
