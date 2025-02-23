import { useState, useEffect } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { useLocation, useNavigate } from "react-router-dom";
import { newtonsCradle } from "ldrs";
import { FaBed, FaBath, FaHome, FaRulerCombined, FaDollarSign, FaTools, FaHammer, FaClipboard } from "react-icons/fa";

export function Result() {
    newtonsCradle.register();
    const [show, setShow] = useState();
    const [data2, setData2] = useState();
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
                setShow(result);
                console.log(result);
            } catch (err) {
                console.error(err);
            }
        };

        fetchText();
    }, []);

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <h1 className="text-2xl font-bold mb-4">Property Assessment</h1>
            {show ? (
                <>
                    <div className="flex flex-col justify-center space-y-4">
                        <div className="flex flex-row items-center space-x-4">
                            <FaBed className="text-xl" />
                            <p className="text-lg font-medium">Bedrooms: {show?.bedrooms}</p>
                            <FaBath className="text-xl" />
                            <p className="text-lg font-medium">Bathrooms: {show?.bathrooms}</p>
                        </div>
                        <div className="flex flex-row items-center space-x-4">
                            <FaHome className="text-xl" />
                            <p className="text-lg font-medium">Property Type: {show?.property_type}</p>
                            <FaRulerCombined className="text-xl" />
                            <p className="text-lg font-medium">Area: {show?.square_feet} sqft</p>
                        </div>
                    </div>
                    <div className="mt-6">
                        <h2 className="text-xl font-semibold">Cost Range</h2>
                        <div className="flex flex-row items-center space-x-4">
                            <FaDollarSign className="text-xl" />
                            <p className="text-lg">Max: ${show?.assessment[0].total_cost_range.max}</p>
                            <FaDollarSign className="text-xl" />
                            <p className="text-lg">Min: ${show?.assessment[0].total_cost_range.min}</p>
                        </div>
                    </div>
                    <div className="mt-6">
                        <h2 className="text-xl font-semibold">Breakdown</h2>
                        <div className="mt-2">
                            <h3 className="text-lg font-medium flex items-center">
                                <FaTools className="mr-2" /> Additional Costs
                            </h3>
                            <p className="text-lg">Max: ${show?.assessment[0].breakdown["Additional Costs"].max}</p>
                            <p className="text-lg">Min: ${show?.assessment[0].breakdown["Additional Costs"].min}</p>
                        </div>
                        <div className="mt-2">
                            <h3 className="text-lg font-medium flex items-center">
                                <FaHammer className="mr-2" /> Labor
                            </h3>
                            <p className="text-lg">Max: ${show?.assessment[0].breakdown["Labor"].max}</p>
                            <p className="text-lg">Min: ${show?.assessment[0].breakdown["Labor"].min}</p>
                        </div>
                        <div className="mt-2">
                            <h3 className="text-lg font-medium flex items-center">
                                <FaClipboard className="mr-2" /> Materials
                            </h3>
                            <p className="text-lg">Max: ${show?.assessment[0].breakdown["Materials"].max}</p>
                            <p className="text-lg">Min: ${show?.assessment[0].breakdown["Materials"].min}</p>
                        </div>
                        <div className="mt-2">
                            <h3 className="text-lg font-medium flex items-center">
                                <FaClipboard className="mr-2" /> Notes
                            </h3>
                            <p className="text-lg">{show?.assessment[0].breakdown.notes}</p>
                        </div>
                    </div>
                </>
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
                            <l-newtons-cradle size="78" speed="1.2" color="#0c0a09"></l-newtons-cradle>
                            <p className="mt-2 p-2 font-mono animate-pulse rounded-md">Loading...</p>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}
