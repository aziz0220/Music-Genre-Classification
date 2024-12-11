"use client";

import { useState } from "react";
import { experimental_useObject } from "ai/react";
import { questionsSchema } from "@/lib/schemas";
import { z } from "zod";
import { toast } from "sonner";
import { FileUp, Plus, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@headlessui/react";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
//import Quiz from "@/components/quiz";
import { Link } from "@/components/ui/link";
import NextLink from "next/link";
import { generateQuizTitle } from "./actions";
import { AnimatePresence, motion } from "framer-motion";
import { VercelIcon, GitIcon } from "@/components/icons";

export default function ChatWithFiles() {
  const [files, setFiles] = useState<File[]>([]);
  const [questions, setQuestions] = useState<z.infer<typeof questionsSchema>>(
    [],
  );
  const [genre, setGenre] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [service, setService] = useState(0);


   const toggleService = () => {
    setService((prev) => (prev === 0 ? 1 : 0));
  };
  // Wrapper for classification logic
  const useClassifyGenre = () => {
    const submit = async ({ files }: { files: { data: File }[] }) => {
      setIsLoading(true);
      let fakeProgress = 0;
      const intervalId = setInterval(() => {
      fakeProgress += 5;
      setProgress(fakeProgress);
      
      if(fakeProgress >= 100){
        clearInterval(intervalId);
        }
      }, 100);
      try {
        // Process the first file (adjust as needed for multiple files)
        const detectedGenre = await classifyGenre(files[0].data);
        setGenre(detectedGenre);
        toast.success(`Genre classified: ${detectedGenre}`);
      } catch (error: any) {
        toast.error(`Error: ${error.message}`);
      } finally {
        setIsLoading(false);
      }
    };

    return {
      submit,
      isLoading,
    };
  };
  const [isDragging, setIsDragging] = useState(false);
  const [title, setTitle] = useState<string>();

  const classifyGenre = async (wavFile: File): Promise<string> => {
    const formData = new FormData();
    formData.append("wav_file", wavFile);
    const serviceUrl = service === 0
      ? "http://localhost:5001/classify_genre"
      : "http://localhost:5002/vgg19_service";
    try {
      const response = await fetch(serviceUrl , {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorDetails = await response.json();
        throw new Error(`Error: ${errorDetails.description}`);
      }

      const result = await response.json();
      console.log(result);
      return result.genre;
    } catch (error: any) {
      console.error("Error classifying genre:", error.message);
      throw error;
    }
  };


  const { submit } = useClassifyGenre();

 // const {
  //  submit,
 //   object: partialQuestions,
 //   isLoading,
 // } = experimental_useObject({
  //  api: "/api/generate-quiz",
 //   schema: questionsSchema,
  //  initialValue: undefined,
  //  onError: (error) => {
  //    toast.error("Failed to generate quiz. Please try again.");
  //    setFiles([]);
  //  },
  //  onFinish: ({ object }) => {
  //    setQuestions(object ?? []);
  //  },
  //});

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);

    if (isSafari && isDragging) {
      toast.error(
        "Safari does not support drag & drop. Please use the file picker.",
      );
      return;
    }

    const selectedFiles = Array.from(e.target.files || []);
    const validFiles = selectedFiles.filter(
      (file) => file.type === "audio/wav" && file.size <= 50 * 1024 * 1024,
    );
    console.log(validFiles);

    if (validFiles.length !== selectedFiles.length) {
      toast.error("Only WAV files under 50MB are allowed.");
    }

    setFiles(validFiles);
  };

  //const encodeFileAsBase64 = (file: File): Promise<string> => {
   //  return new Promise((resolve, reject) => {
      // const reader = new FileReader();
  //     reader.readAsDataURL(file);
  //     reader.onload = () => resolve(reader.result as string);
   //    reader.onerror = (error) => reject(error);
   //  });
   //};

 const handleSubmitWithFiles = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const encodedFiles = files.map((file) => ({ name: file.name, type: file.type, data: file }));
    submit({ files: encodedFiles });
  };

  const clearPDF = () => {
    setFiles([]);
    setQuestions([]);
  };


 // if (!isLoading) {
 //   return (
 //     <Quiz title={title ?? "GENRE"} questions={questions} clearPDF={clearPDF} />
//    );
//  }

  return (
    <div
      className="min-h-[100dvh] w-full flex justify-center"
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragExit={() => setIsDragging(false)}
      onDragEnd={() => setIsDragging(false)}
      onDragLeave={() => setIsDragging(false)}
      onDrop={(e) => {
        e.preventDefault();
        setIsDragging(false);
        console.log(e.dataTransfer.files);
        handleFileChange({
          target: { files: e.dataTransfer.files },
        } as React.ChangeEvent<HTMLInputElement>);
      }}
    >
      <AnimatePresence>
        {isDragging && (
          <motion.div
            className="fixed pointer-events-none dark:bg-zinc-900/90 h-dvh w-dvw z-10 justify-center items-center flex flex-col gap-1 bg-zinc-100/90"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div>Drag and drop files here</div>
            <div className="text-sm dark:text-zinc-400 text-zinc-500">
              {"(WAVs only)"}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      <Card className="w-full max-w-md h-full border-0 sm:border sm:h-fit mt-12">
        <CardHeader className="text-center space-y-6">
          <div className="mx-auto flex items-center justify-center space-x-2 text-muted-foreground">
            <div className="rounded-full bg-primary/10 p-2">
              <FileUp className="h-6 w-6" />
            </div>
            <Plus className="h-4 w-4" />
            <div className="rounded-full bg-primary/10 p-2">
              <Loader2 className="h-6 w-6" />
            </div>
          </div>
          <div className="space-y-2">
            <CardTitle className="text-2xl font-bold">
            Music Genre Classifier
            </CardTitle>
            <CardDescription className="text-base">
              Upload a WAV file to predict the music genre.
            </CardDescription>
             <div className="flex items-center justify-center space-x-4">
        <span>SVM</span>
        <Switch
          checked={service === 1}  // If service is 1, use VGG
          onChange={toggleService}
          className="relative inline-flex items-center h-6 rounded-full w-11"
        >
          <span className="sr-only">Use VGG Model</span>
          <span
            className={`${
              service === 1 ? "translate-x-6" : "translate-x-1"
            } inline-block w-4 h-4 transform bg-white rounded-full transition`}
          />
        </Switch>
        <span>VGG</span>
      </div>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmitWithFiles} className="space-y-4">
            <div
              className={`relative flex flex-col items-center justify-center border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 transition-colors hover:border-muted-foreground/50`}
            >
              <input
                type="file"
                onChange={handleFileChange}
                accept="audio/wav"
                className="absolute inset-0 opacity-0 cursor-pointer"
              />
              <FileUp className="h-8 w-8 mb-2 text-muted-foreground" />
              <p className="text-sm text-muted-foreground text-center">
                {files.length > 0 ? (
                  <span className="font-medium text-foreground">
                    {files[0].name}
                  </span>
                ) : (
                  <span>Drop your WAV here or click to browse.</span>
                )}
              </p>
            </div>
            <Button
              type="submit"
              className="w-full"
              disabled={files.length === 0}
            >
              {isLoading ? (
                <span className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Generating Response...</span>
                </span>
              ) : (
                "Predict Genre"
              )}
            </Button>
          </form>
        </CardContent>
        {isLoading && (
          <CardFooter className="flex flex-col space-y-4">
            <div className="w-full space-y-1">
              <div className="flex justify-between text-sm text-muted-foreground">
                <span>Progress</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>
            <div className="w-full space-y-2">
              <div className="grid grid-cols-6 sm:grid-cols-4 items-center space-x-2 text-sm">
                <div
                  className={`h-2 w-2 rounded-full ${
                    isLoading ? "bg-yellow-500/50 animate-pulse" : "bg-muted"
                  }`}
                />
                <span className="text-muted-foreground text-center col-span-4 sm:col-span-2">
                  
                  Extracting Features, 
                   Analyzing WAV content
                </span>
              </div>
            </div>
          </CardFooter>
        )}
      </Card>
      <motion.div
        className="flex flex-row gap-4 items-center justify-between fixed bottom-6 text-xs "
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
      >
        <NextLink
          target="_blank"
          href="https://github.com/aziz0220/Mini-Projet-Docker"
          className="flex flex-row gap-2 items-center border px-2 py-1.5 rounded-md hover:bg-zinc-100 dark:border-zinc-800 dark:hover:bg-zinc-800"
        >
          <GitIcon />
          View Source Code
        </NextLink>

        <NextLink
          target="_blank"
          href="https://www.linkedin.com/in/aziz-benamor/"
          className="flex flex-row gap-2 items-center bg-zinc-900 px-2 py-1.5 rounded-md text-zinc-50 hover:bg-zinc-950 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-50"
        >
          <VercelIcon size={14} />
          LinkedIn
        </NextLink>
      </motion.div>
    </div>
  );
}
