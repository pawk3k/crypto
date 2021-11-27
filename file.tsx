
const useConnectPlaid = (): [PlaidConnect, PlaidConnectState] => {
  const [state, setState] = useState<PlaidConnectState>({
    isLoading: false,
    isConnected: false,
    isError: false,
    error: null,
  });

  const connectPlaid = useCallback(
    async (
      publicKey: string,
      env: PlaidEnv,
      product: PlaidProduct[],
      options: PlaidOptions,
    ) => {
      setState({
        isLoading: true,
        isConnected: false,
        isError: false,
        error: null,
      });

      try {
        const { public_token, metadata } = await Plaid.create({
          ...options,
          env,
          product,
          key: publicKey,
        });

        setState({
          isLoading: false,
          isConnected: true,
          isError: false,
          error: null,
          publicToken: public_token,
          metadata,
        });
      } catch (error) {
        setState({
          isLoading: false,
          isConnected: false,
          isError: true,
          error,
        });
      }
    },
    [],
  );

  return [connectPlaid, state];
}; 



