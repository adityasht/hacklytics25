import { useState, useEffect } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { useLocation, useNavigate } from "react-router-dom";

export function Result() {
    const [text, setText] = useState<string | null>(null);
    const location = useLocation();
    const navigate = useNavigate();
    const data = location.state;
    useEffect(() => {
        if (data) {
            console.log(data);
        } else {
            console.log("No data found");
            navigate("/");
        }

        const fetchText = async () => {
            await new Promise((resolve) => setTimeout(resolve, 5000));
            //make post req to api

            const loremIpsum =
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi.";

            setText(loremIpsum);
        };

        fetchText();
    }, []);

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <h1 className="text-2xl font-bold mb-4">Lorem ipsum</h1>
            {text ? (
                <p>{text}</p>
            ) : (
                <div className="space-y-2">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-3/4" />
                </div>
            )}
        </div>
    );
}
