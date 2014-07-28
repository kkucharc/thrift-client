//================ RESPONSES =========================
// statusy operacji 
enum ResponseStatus {
	OK = 1,
	BAD_REQUEST = 2,
	FILE_NOT_FOUND = 3,
	FILE_ALREADY_EXIST = 4,
	IO_ERROR = 5,
	CANNOT_REMOVE_FILE = 6,
    SERVICE_INTERNAL_PROBLEM = 7
	// TODO wszelkie statusy beledow w tym enumie
}

// w odpowiedzi przesyłany jest plik
// 1: jesli nie ma błedu to zawsze OK
// 2: nazwa pliku
// 3: plik
struct GetFileResponse {
	1: required ResponseStatus status,		
	2: optional string fileName,				
	3: optional binary fileData					
}

// jesli nie ma błedu to zawsze OK
struct AddFileResponse {
	1: required ResponseStatus status		
}

// jesli nie ma błedu to zawsze OK
struct RemoveFileResponse {
	1: required ResponseStatus status						
}

// jesli nie ma błedu to zawsze OK
struct MoveFileResponse {
	1: required ResponseStatus status;						
}

// jesli nie ma błedu to zawsze OK
// lista sciezek
struct ListDirResponse {
	1: required ResponseStatus status,						
	2: optional list<string> result							
}

// status pliku, status kopiwania, przenoszenia itp.
//TODO pomyslec nad tym
struct FileStatusResponse {
	1: required ResponseStatus status,
	2: optional i32 progres									
}

//=================== REQUESTS =========================
// sciezka do pliku na serwerze
// nazwa pliku
// plik
// rozmiar pliku
struct AddFileRequest {
	1: required string serverPath,				 			
	2: required string fileName,							
	3: required binary fileData,							
	4: optional i32 fileSize								
}

// sciezka pliku na serwerze
struct GetFileRequest {
	1: required string serverPath							
}

// sciezka pliku na serwerze
struct RemoveFileRequest {
	1: required string serverPath							
}

// aktualna sciezka
// nowa sciezka
struct MoveFileRequest {
	1: required string currentPath,							
	2: required string newPath								
}

struct ListDirRequest {
	1: required string dirPath								
}

//1: dodanie pliku
//2: pobranie istniejacego pliku
//3: usuniecie pliku z serwera
//4: przeniesienie pliku w inne miejsce
//5: wylistowanie katalogu
service FileResourceService {
	AddFileResponse addFile(1: AddFileRequest request),
	GetFileResponse getFile(1: GetFileRequest request),
	RemoveFileResponse removeFile(1: RemoveFileRequest request),
	MoveFileResponse moveFile(1: MoveFileRequest request),
	ListDirResponse listDir(1: ListDirRequest request),
}

// metody testowe do sprawdzania polaczenia
// 1: ping
// 2: przywitanie
service HelloFriend {
    void ping(),
    string sayHello(),
}