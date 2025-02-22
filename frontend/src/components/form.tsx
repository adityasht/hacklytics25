"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { toast } from "sonner";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";

import { Textarea } from "@/components/ui/textarea";

import { useNavigate } from "react-router-dom";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED_IMAGE_TYPES = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
];

const formSchema = z.object({
    address: z.string().min(1, { message: "Address is required." }),
    damageContext: z
        .string()
        .max(500, {
            message: "Damage context must be less than 500 characters.",
        })
        .optional(),

    retrofitContext: z
        .string()
        .max(500, {
            message: "Retrofit context must be less than 500 characters.",
        })
        .optional(),
});

type FormValues = z.infer<typeof formSchema>;
export function LocationForm() {
    const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
    const [selectedRetrofit, setSelectedRetrofit] = useState<File[]>([]);
    const navigate = useNavigate();
    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            address: "",
            damageContext: "",
            retrofitContext: "",
        },
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        if (selectedFiles.length == 0) {
            toast.error("Please select an image.", {
                style: { backgroundColor: "red", color: "white" },
            });
            return;
        }
        if (selectedFiles.some((file) => file.size > MAX_FILE_SIZE)) {
            toast.error("File size is too large. Max size is 5MB.", {
                style: { backgroundColor: "red", color: "white" },
            });
            return;
        }
        if (
            selectedFiles.some(
                (file) => !ACCEPTED_IMAGE_TYPES.includes(file.type)
            )
        ) {
            toast.error(
                "Invalid file type. Only JPEG, PNG, and WEBP allowed.",
                {
                    style: { backgroundColor: "red", color: "white" },
                }
            );
            return;
        }
        if (selectedRetrofit.some((file) => file.size > MAX_FILE_SIZE)) {
            toast.error("File size is too large. Max size is 5MB.", {
                style: { backgroundColor: "red", color: "white" },
            });
            return;
        }
        if (
            selectedRetrofit.some(
                (file) => !ACCEPTED_IMAGE_TYPES.includes(file.type)
            )
        ) {
            toast.error(
                "Invalid file type. Only JPEG, PNG, and WEBP allowed.",
                {
                    style: { backgroundColor: "red", color: "white" },
                }
            );
            return;
        }
        const data = {
            ...values,
            images: selectedFiles,
            retrofit: selectedRetrofit,
        };
        console.log(data);
        toast.success("Form submitted!", {
            description: "Redirecting to results page.",
        });
        navigate("/results", { state: data });
    }

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (files) {
            setSelectedFiles(Array.from(files));
        }
    };
    const handleRetrofitChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const files = e.target.files;
        if (files) {
            setSelectedRetrofit(Array.from(files));
        }
    };
    return (
        <Card className="w-[550px]">
            <CardHeader>
                <CardTitle>Property Information</CardTitle>
                <CardDescription>
                    Enter details about your property below
                </CardDescription>
            </CardHeader>
            <CardContent>
                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="space-y-8">
                        <FormField
                            control={form.control}
                            name="address"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Address</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="Enter your property address"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        Enter the address of your property
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormItem>
                            <FormLabel>Upload Images of any damages</FormLabel>
                            <FormControl>
                                <Input
                                    type="file"
                                    multiple
                                    accept="image/*"
                                    onChange={handleFileChange}
                                />
                            </FormControl>
                            <FormDescription>
                                {selectedFiles.length > 0
                                    ? "Selected files: " +
                                      selectedFiles
                                          .map((file) => file.name)
                                          .join(", ")
                                    : "Choose images to upload"}
                            </FormDescription>
                            <FormMessage />
                        </FormItem>

                        <FormField
                            control={form.control}
                            name="damageContext"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Damages Context</FormLabel>
                                    <FormControl>
                                        <Textarea
                                            placeholder="Provide some context about the damages (optional)"
                                            className="resize-none"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        Describe the damages or provide any
                                        additional information (max 500
                                        characters)
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormItem>
                            <FormLabel>
                                Upload Images of any retrofits/upgrades{" "}
                            </FormLabel>
                            <FormControl>
                                <Input
                                    type="file"
                                    multiple
                                    accept="image/*"
                                    onChange={handleRetrofitChange}
                                />
                            </FormControl>
                            <FormDescription>
                                {selectedRetrofit.length > 0
                                    ? "Selected files: " +
                                      selectedRetrofit
                                          .map((file) => file.name)
                                          .join(", ")
                                    : "Choose images to upload"}
                            </FormDescription>
                        </FormItem>
                        <FormField
                            control={form.control}
                            name="retrofitContext"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Retrofits Context</FormLabel>
                                    <FormControl>
                                        <Textarea
                                            placeholder="Provide some context about the retrofits (optional)"
                                            className="resize-none"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormDescription>
                                        Describe the retrofits or provide any
                                        additional information (max 500
                                        characters)
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <Button type="submit">Submit</Button>
                    </form>
                </Form>
            </CardContent>
        </Card>
    );
}
