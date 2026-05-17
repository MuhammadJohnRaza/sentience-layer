/** * Hook
for insight feed with filtering */
import { useState, useEffect, useCallback } from "react";
import { Insight } from "@/types";
import { api } from "@/lib/api";
export function useInsights(initialFilters?: any) {
  const [insights, setInsights] = useState<Insight[]>([]);
  const [filters, setFilters] = useState(initialFilters || {});
  const [isLoading, setIsLoading] = useState(true);
  const fetchInsights = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await api.getInsights(filters);
      setInsights(data);
    } catch (error) {
      console.error("Failed to fetch insights:", error);
    } finally {
      setIsLoading(false);
    }
  }, [filters]);
  useEffect(() => {
    fetchInsights();
  }, [fetchInsights]);
  const refresh = useCallback(() => fetchInsights(), [fetchInsights]);
  const filterByType = useCallback((type: string) => {
    setFilters((prev: any) => ({
      ...prev,
      type,
    }));
  }, []);
  const filterBySeverity = useCallback((severity: string) => {
    setFilters((prev: any) => ({
      ...prev,
      severity,
    }));
  }, []);
  return {
    insights,
    isLoading,
    filters,
    refresh,
    filterByType,
    filterBySeverity,
  };
}
