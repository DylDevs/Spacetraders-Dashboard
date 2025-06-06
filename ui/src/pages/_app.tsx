import type { AppProps } from 'next/app';
import { ThemeProvider } from '@/components/theme_provider';
import { Loading } from '@/components/loading';
import { useEffect, useState } from 'react'; 
import { toast, Toaster } from 'sonner';
import { Metadata } from 'next';
import { AttemptServerConnection } from '@/components/webserver';
import '@/styles/globals.css';

// @ts-ignore | Prevents module not found error from js-cookie, even though it is installed
import Cookies from 'js-cookie';

export const metadata: Metadata = {
    title: "Spacetraders Dashboard",
    description: "Dashboard to visualize your fleet and navigate the universe in Spacetraders",
    icons: ["favicon.ico"],
};

export default function App({ Component, pageProps }: AppProps) {
  const [showLoading, setShowLoading] = useState(true);

  const setupConnection = async () => {
    try {
      const webserver_url = "http://localhost:8000";
      const connected = await AttemptServerConnection(webserver_url);
    
      Cookies.set("connected", connected ? "true" : "false");

      if (!connected) {
        throw new Error("Failed to connect to server");
      }
    } catch (error) {
      throw error;
    }
  };

  useEffect(() => {
    toast.promise(
      new Promise<void>(async (resolve, reject) => {
        try {
          await setupConnection();
          setTimeout(() => {
            setShowLoading(false);
            resolve();
          }, 1000);
          console.log("Connected to training server at " + Cookies.get("webserver_url"));
        } catch (error) {
          reject(error);
          console.log(error);
          setShowLoading(false);
        }
      }),
      {
        loading: "Connecting to server...",
        success: "Connected to server!",
        error: "Failed to connect to server",
      }
    );
  }, []);

  return (
    <ThemeProvider defaultTheme="dark" attribute="class">
      <Toaster position="bottom-right" theme="dark" closeButton={true} duration={5000} />
      <div>
        {showLoading && <Loading loading_text="Connecting to server..." fullscreen />}
        <div style={{ display: showLoading ? "none" : "block" }} className='overflow-hidden'>
          <Component {...pageProps} />
        </div>
      </div>
    </ThemeProvider>
  );
}