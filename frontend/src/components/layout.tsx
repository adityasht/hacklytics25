import { Outlet } from "react-router-dom";

interface LayoutProps {
    children?: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
    return (
        <div className="flex flex-col items-center justify-center h-max p-1 bg-gray-100">
            <div className="w-full max-w-2xl p-5">
                <main>{children || <Outlet />}</main>
            </div>
        </div>
    );
};
