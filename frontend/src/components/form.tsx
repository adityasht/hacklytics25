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
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

import { Textarea } from "@/components/ui/textarea";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED_IMAGE_TYPES = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
];

const formSchema = z.object({
    zipCode: z.string().length(5, {
        message: "Zip code must be 5 characters.",
    }),
    neighborhood: z.string().min(2, {
        message: "Neighborhood must be at least 2 characters.",
    }),
    propertyType: z.enum(
        [
            "Condo",
            "Land",
            "Manufactured",
            "Multi-Family",
            "Single Family",
            "Townhouse",
        ],
        {
            required_error: "Please select a property type.",
        }
    ),
    bedrooms: z.number().min(1).max(5),
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
    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            zipCode: "",
            neighborhood: "",
            propertyType: undefined,
            bedrooms: 1,
        },
    });

    function onSubmit(values: z.infer<typeof formSchema>) {
        console.log(values);
        if (selectedFiles.length == 0) {
            toast.error("Please select an image.");
        }
        if (selectedFiles.some((file) => file.size > MAX_FILE_SIZE)) {
            toast.error("File size is too large. Max size is 5MB.");
        }
        if (
            selectedFiles.some(
                (file) => !ACCEPTED_IMAGE_TYPES.includes(file.type)
            )
        ) {
            toast.error("Invalid file type. Only JPEG, PNG, and WEBP allowed.");
        }
        if (selectedRetrofit.some((file) => file.size > MAX_FILE_SIZE)) {
            toast.error("File size is too large. Max size is 5MB.");
        }
        if (
            selectedRetrofit.some(
                (file) => !ACCEPTED_IMAGE_TYPES.includes(file.type)
            )
        ) {
            toast.error("Invalid file type. Only JPEG, PNG, and WEBP allowed.");
        }
        console.log({
            ...values,
            images: selectedFiles,
            retrofit: selectedRetrofit,
        });
        toast.success("Form submitted!", {
            description: "Check the console for form data.",
        });
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
                            name="zipCode"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Zip Code</FormLabel>
                                    <FormControl>
                                        <Input
                                            type="text"
                                            maxLength={5}
                                            placeholder="Enter zip code"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="neighborhood"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Neighborhood</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="Enter neighborhood"
                                            {...field}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="propertyType"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Property Type</FormLabel>
                                    <Select
                                        onValueChange={field.onChange}
                                        defaultValue={field.value}>
                                        <FormControl>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select a property type" />
                                            </SelectTrigger>
                                        </FormControl>
                                        <SelectContent>
                                            <SelectItem value="Condo">
                                                Condo
                                            </SelectItem>
                                            <SelectItem value="Land">
                                                Land
                                            </SelectItem>
                                            <SelectItem value="Manufactured">
                                                Manufactured
                                            </SelectItem>
                                            <SelectItem value="Multi-Family">
                                                Multi-Family
                                            </SelectItem>
                                            <SelectItem value="Single Family">
                                                Single Family
                                            </SelectItem>
                                            <SelectItem value="Townhouse">
                                                Townhouse
                                            </SelectItem>
                                        </SelectContent>
                                    </Select>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />
                        <FormField
                            control={form.control}
                            name="bedrooms"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Bedrooms</FormLabel>
                                    <FormControl>
                                        <div className="flex items-center space-x-2">
                                            <Button
                                                type="button"
                                                variant="outline"
                                                size="icon"
                                                onClick={() => {
                                                    if (!field.value) {
                                                        field.onChange(1);
                                                    } else if (
                                                        field.value > 1
                                                    ) {
                                                        field.onChange(
                                                            field.value - 1
                                                        );
                                                    }
                                                }}>
                                                -
                                            </Button>
                                            <Input
                                                type="number"
                                                {...field}
                                                onChange={(e) => {
                                                    const value =
                                                        Number.parseInt(
                                                            e.target.value
                                                        );
                                                    field.onChange(
                                                        Math.min(
                                                            Math.max(1, value),
                                                            5
                                                        )
                                                    );
                                                }}
                                                className="w-16 text-center"
                                            />
                                            <Button
                                                type="button"
                                                variant="outline"
                                                size="icon"
                                                onClick={() => {
                                                    if (!field.value) {
                                                        field.onChange(1);
                                                    } else if (
                                                        field.value < 5
                                                    ) {
                                                        field.onChange(
                                                            field.value + 1
                                                        );
                                                    }
                                                }}>
                                                +
                                            </Button>
                                        </div>
                                    </FormControl>
                                    <FormDescription>
                                        Number of bedrooms (1-5)
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
                                    <FormLabel>Retorfits Context</FormLabel>
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
