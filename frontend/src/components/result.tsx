import { useState, useEffect } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { useLocation, useNavigate } from "react-router-dom";
import { newtonsCradle } from "ldrs";

export function Result() {
    newtonsCradle.register();
    const [text, setText] = useState<string | null>(null);
    const location = useLocation();
    const navigate = useNavigate();
    const data = location.state;
    useEffect(() => {
        console.log("in effect");
        if (!data) {
            navigate("/");
        }

        const fetchText = async () => {
            const formData = new FormData();
            formData.append("address", data.address);
            formData.append("damageContext", data.damage);
            data.images.forEach((image: File, index: number) => {
                formData.append(`image${index}`, image);
            });
            data.retrofit.forEach((file: File, index: number) => {
                formData.append(`retrofit${index}`, file);
            });
            try {
                console.log("fetching");
                const response = await fetch("http://localhost:5000/", {
                    method: "POST",
                    body: formData,
                });
                const result = await response.json();
                console.log(result);
            } catch (err) {
                console.error(err);
            }
        };

        fetchText();
    }, []);

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <h1 className="text-2xl font-bold mb-4">Lorem ipsum</h1>
            {text ? (
                <p>{text}</p>
            ) : (
                <>
                    <div className="space-y-2">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-3/4" />
                    </div>
                    <div className="flex justify-center mt-4">
                        <div className="flex w-1 flex-col items-center">
                            <l-newtons-cradle
                                size="78"
                                speed="1.2"
                                color="#0c0a09"></l-newtons-cradle>
                            <p className="mt-2 p-2 font-mono animate-pulse rounded-md">
                                Loading...
                            </p>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}
