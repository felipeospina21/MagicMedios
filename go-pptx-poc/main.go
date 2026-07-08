package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/duynguyendang/docxgo/v3/pptx"
)

type Client struct {
	Name    string
	Company string
}

type Representative struct {
	Name  string
	Phone string
	Email string
}

type Contact struct {
	Address string
	Web     string
	Phone   string
	Email   string
}

type ColorInventory struct {
	Color     string
	Inventory string
}

type ProductData struct {
	Ref            string
	Title          string
	Subtitle       string
	Description    []string
	ImagePath      string
	ColorInventory []ColorInventory
}

type QuoteData struct {
	Client         Client
	Representative Representative
	Contact        Contact
	Consecutive    int
	Products       []ProductData
	OutputPath     string
	LogoPath       string
	PolicyPath     string
}

const (
	xScale     = 25.4 / 21.0
	yScale     = 19.05 / 29.7
	textScale  = 0.85
	pageBottom = 18.15
)

func main() {
	if err := run(); err != nil {
		log.Fatal(err)
	}
}

func run() error {
	data := mockData()

	pres := pptx.NewPresentation()
	pres.SetTitle("Magic Medios POC")
	pres.SetAuthor("Magic Medios")
	pres.SetLayout(pptx.Layout4x3)

	slideCount := len(data.Products) + 1
	for i := 0; i < slideCount; i++ {
		slide := pres.AddSlide()
		slide.SetBackgroundColor(pptx.White)

		addLogo(slide, data.LogoPath)
		addFooter(slide, data.Contact)

		if i == slideCount-1 {
			addPolicySlide(slide, data.PolicyPath)
			continue
		}

		product := data.Products[i]
		if i == 0 {
			addHeader(slide, data.Representative, data.Consecutive)
			addClientName(slide, data.Client)
		}

		addProductContent(slide, product)
	}

	if err := os.MkdirAll(filepath.Dir(data.OutputPath), 0o755); err != nil {
		return err
	}

	if err := pres.SaveAs(data.OutputPath); err != nil {
		return err
	}

	fmt.Println("pptx written to:", data.OutputPath)
	return nil
}

func mockData() QuoteData {
	return QuoteData{
		Client: Client{
			Name:    "Juan Pérez",
			Company: "Nutresa",
		},
		Representative: Representative{
			Name:  "Felipe Ospina",
			Phone: "300 123 4567",
			Email: "felipe@magicmedios.com",
		},
		Contact: Contact{
			Address: "Calle 123 #45-67",
			Web:     "www.magicmedios.com",
			Phone:   "300 123 4567",
			Email:   "ventas@magicmedios.com",
		},
		Consecutive: 1042,
		Products: []ProductData{
			{
				Ref:      "cpMU-12-2",
				Title:    "Mug de ceramica",
				Subtitle: "Con empaque individual",
				Description: []string{
					"Capacidad 11 oz",
					"Acabado blanco brillante",
					"Incluye impresión a un color",
				},
				ImagePath: filepath.Join("..", "images", "logo.jpeg"),
				ColorInventory: []ColorInventory{
					{Color: "Blanco", Inventory: "120"},
					{Color: "Negro", Inventory: "85"},
					{Color: "Azul", Inventory: "43"},
				},
			},
			{
				Ref:   "mpGO0020",
				Title: "Botella deportiva",
				Description: []string{
					"Tapa de rosca",
					"Material PET",
					"Capacidad 750 ml",
				},
				ImagePath: filepath.Join("..", "images", "logo.jpeg"),
				ColorInventory: []ColorInventory{
					{Color: "Rojo", Inventory: "68"},
					{Color: "Verde", Inventory: "54"},
				},
			},
		},
		OutputPath: filepath.Join("..", "cotizaciones", "go_poc_cotizacion.pptx"),
		LogoPath:   filepath.Join("..", "images", "logo.jpeg"),
		PolicyPath: filepath.Join("..", "images", "condiciones.jpeg"),
	}
}

func addLogo(slide *pptx.Slide, path string) {
	img, err := os.ReadFile(path)
	if err != nil {
		return
	}

	slide.AddImage(img).
		SetPosition(cx(1), cy(0.5)).
		SetSize(cw(8.9), ch(1.7))
}

func addFooter(slide *pptx.Slide, contact Contact) {
	footer := strings.TrimSpace(
		fmt.Sprintf("%s %s %s %s", contact.Address, contact.Phone, contact.Email, contact.Web),
	)

	slide.AddText(footer).
		SetFontFamily("Arial").
		SetFontSize(s(6)).
		SetAlignment(pptx.AlignmentCenter).
		SetPosition(cx(0.5), cy(pageBottom)).
		SetSize(cw(18), ch(0.7)).
		SetColor(pptx.Black).
		SetFillColor(pptx.White)
}

func addHeader(slide *pptx.Slide, rep Representative, consecutive int) {
	lines := []string{
		spanishDate(time.Now()),
		fmt.Sprintf("Cot N°%d", consecutive),
		"",
		"Asesor Comercial",
		fmt.Sprintf("%s %s %s", rep.Name, rep.Phone, rep.Email),
	}

	slide.AddText(strings.Join(lines, "\n")).
		SetFontFamily("Arial").
		SetFontSize(s(12)).
		SetPosition(cx(11.0), cy(0.35)).
		SetSize(cw(7.4), ch(4.3)).
		SetColor(pptx.Black).
		SetFillColor(pptx.White)
}

func addClientName(slide *pptx.Slide, client Client) {
	text := fmt.Sprintf("Señor(a) %s.\n%s", client.Name, client.Company)

	slide.AddText(text).
		SetFontFamily("Arial").
		SetFontSize(s(13)).
		SetBold(true).
		SetPosition(cx(1), cy(1.7)).
		SetSize(cw(6.4), ch(1.7)).
		SetColor(pptx.Black).
		SetFillColor(pptx.White)
}

func addProductContent(slide *pptx.Slide, product ProductData) {
	title := fmt.Sprintf("1. %s %s", product.Title, product.Ref)
	slide.AddText(title).
		SetFontFamily("Arial").
		SetFontSize(s(11)).
		SetBold(true).
		SetPosition(cx(0.8), cy(3.1)).
		SetSize(cw(17.0), ch(0.7)).
		SetColor(pptx.Black).
		SetFillColor(pptx.White)

	if product.Subtitle != "" {
		slide.AddText(product.Subtitle).
			SetFontFamily("Arial").
			SetFontSize(s(10)).
			SetPosition(cx(0.8), cy(3.85)).
			SetSize(cw(17.0), ch(1.0)).
			SetColor(pptx.Black).
			SetFillColor(pptx.White)
	}

	slide.AddText(strings.Join(product.Description, "\n")).
		SetFontFamily("Arial").
		SetFontSize(s(10)).
		SetPosition(cx(0.8), cy(4.9)).
		SetSize(cw(17.0), ch(3.0)).
		SetColor(pptx.Black).
		SetFillColor(pptx.White)

	addProductImage(slide, product.ImagePath)
	addQuantityTable(slide)
	addInventoryTable(slide, product.ColorInventory)
}

func addPolicySlide(slide *pptx.Slide, path string) {
	img, err := os.ReadFile(path)
	if err != nil {
		return
	}

	slide.AddImage(img).
		SetPosition(cx(1), cy(4.2)).
		SetSize(cw(17.0), ch(13.0))
}

func addProductImage(slide *pptx.Slide, path string) {
	img, err := os.ReadFile(path)
	if err != nil {
		return
	}

	slide.AddImage(img).
		SetPosition(cx(8.8), cy(7.7)).
		SetSize(cw(6.8), ch(4.3))
}

func addQuantityTable(slide *pptx.Slide) {
	headers := []string{"CANTIDAD", "TÉCNICA DE MARCACIÓN", "DETALLE", "VALOR UNITARIO ANTES DE IVA"}
	widths := []float64{3.0, 5.5, 5.2, 3.7}

	x := 1.2
	y := 11.1
	for idx, header := range headers {
		slide.AddText(header).
			SetBold(true).
			SetFontFamily("Arial").
			SetFontSize(s(7)).
			SetAlignment(pptx.AlignmentCenter).
			SetFillColor(pptx.Color{R: 26, G: 152, B: 139}).
			SetColor(pptx.White).
			SetPosition(cx(x), cy(y)).
			SetSize(cw(widths[idx]), ch(0.45))
		x += widths[idx]
	}

	for row := 0; row < 2; row++ {
		rowY := y + 0.45 + float64(row)*0.45
		values := []string{"(Und)", "", "", "$"}
		x = 1.2
		for idx, value := range values {
			slide.AddText(value).
				SetBold(true).
				SetFontFamily("Arial").
				SetFontSize(s(7)).
				SetAlignment(pptx.AlignmentCenter).
				SetFillColor(pptx.White).
				SetColor(pptx.Black).
				SetPosition(cx(x), cy(rowY)).
				SetSize(cw(widths[idx]), ch(0.4))
			x += widths[idx]
		}
	}
}

func addInventoryTable(slide *pptx.Slide, inventory []ColorInventory) {
	headers := []string{"Color", "Inventario"}
	widths := []float64{3.8, 2.2}

	x := 1.2
	y := 13.2
	for idx, header := range headers {
		slide.AddText(header).
			SetBold(true).
			SetFontFamily("Arial").
			SetFontSize(s(7)).
			SetAlignment(pptx.AlignmentCenter).
			SetFillColor(pptx.White).
			SetColor(pptx.Black).
			SetPosition(cx(x), cy(y)).
			SetSize(cw(widths[idx]), ch(0.45))
		x += widths[idx]
	}

	for row, item := range inventory {
		rowY := y + 0.45 + float64(row)*0.45
		values := []string{item.Color, item.Inventory}
		x = 1.2
		for idx, value := range values {
			slide.AddText(value).
				SetFontFamily("Arial").
				SetFontSize(s(7)).
				SetFillColor(pptx.White).
				SetColor(pptx.Black).
				SetAlignment(pptx.AlignmentLeft).
				SetPosition(cx(x), cy(rowY)).
				SetSize(cw(widths[idx]), ch(0.4))
			x += widths[idx]
		}
	}
}

func spanishDate(t time.Time) string {
	months := []string{
		"enero", "febrero", "marzo", "abril", "mayo", "junio",
		"julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
	}
	return fmt.Sprintf("%d %s de %d", t.Day(), months[int(t.Month())-1], t.Year())
}

func cx(v float64) int64 { return pptx.Cm(v * xScale) }
func cy(v float64) int64 { return pptx.Cm(v * yScale) }
func cw(v float64) int64 { return pptx.Cm(v * xScale) }
func ch(v float64) int64 { return pptx.Cm(v * yScale) }
func s(v int) int        { return int(float64(v) * textScale) }
