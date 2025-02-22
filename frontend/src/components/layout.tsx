import { Outlet } from "react-router-dom";
import { Toaster } from "sonner";

interface LayoutProps {
    children?: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="flex flex-col items-center  min-h-screen p-1 bg-gray-100">
            <div className="w-full max-w-2xl p-5">
                <main>{children || <Outlet />}</main>
                <Toaster />
            </div>
        </div>
    );
};
